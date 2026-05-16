#!/usr/bin/env node

/**
 * 🔱 NEXUS MCP SERVER - ONEDRIVE
 * Servidor MCP para acceso a OneDrive con capacidades de reconstrucción de conversaciones
 * Usa Microsoft Graph API para acceso completo a OneDrive/SharePoint
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { Client } from '@microsoft/microsoft-graph-client';
import { ConfidentialClientApplication } from '@azure/msal-node';
import * as dotenv from 'dotenv';

dotenv.config();

// Configuración
const CLIENT_ID = process.env.ONEDRIVE_CLIENT_ID;
const CLIENT_SECRET = process.env.ONEDRIVE_CLIENT_SECRET;
const TENANT_ID = process.env.ONEDRIVE_TENANT_ID || 'common';
const NEXUS_WORKSPACE = process.env.NEXUS_WORKSPACE || '/Nexus';

if (!CLIENT_ID || !CLIENT_SECRET) {
  console.error('❌ ERROR: Credenciales de OneDrive no configuradas en .env');
  console.error('Necesitas: ONEDRIVE_CLIENT_ID, ONEDRIVE_CLIENT_SECRET');
  process.exit(1);
}

// Configurar MSAL
const msalConfig = {
  auth: {
    clientId: CLIENT_ID,
    authority: `https://login.microsoftonline.com/${TENANT_ID}`,
    clientSecret: CLIENT_SECRET,
  }
};

const cca = new ConfidentialClientApplication(msalConfig);
let graphClient;

// Obtener token de acceso
async function getAccessToken() {
  try {
    const result = await cca.acquireTokenByClientCredential({
      scopes: ['https://graph.microsoft.com/.default'],
    });
    return result.accessToken;
  } catch (error) {
    console.error('Error obteniendo token:', error);
    throw error;
  }
}

// Inicializar cliente Graph
async function initGraphClient() {
  const token = await getAccessToken();
  graphClient = Client.init({
    authProvider: (done) => {
      done(null, token);
    },
  });
}

// Inicializar servidor MCP
const server = new Server(
  {
    name: 'nexus-onedrive-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

/**
 * HERRAMIENTAS DISPONIBLES
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'onedrive_list_files',
        description: 'Lista archivos y carpetas en OneDrive. Útil para explorar exports de conversaciones.',
        inputSchema: {
          type: 'object',
          properties: {
            path: {
              type: 'string',
              description: 'Ruta en OneDrive (por defecto: /Nexus)',
              default: NEXUS_WORKSPACE
            },
            recursive: {
              type: 'boolean',
              description: 'Listar recursivamente',
              default: false
            }
          }
        }
      },
      {
        name: 'onedrive_read_file',
        description: 'Lee contenido de un archivo en OneDrive. Soporta JSON, TXT, MD, HTML, DOCX.',
        inputSchema: {
          type: 'object',
          properties: {
            path: {
              type: 'string',
              description: 'Ruta completa del archivo en OneDrive'
            }
          },
          required: ['path']
        }
      },
      {
        name: 'onedrive_write_file',
        description: 'Escribe o actualiza un archivo en OneDrive.',
        inputSchema: {
          type: 'object',
          properties: {
            path: {
              type: 'string',
              description: 'Ruta completa del archivo en OneDrive'
            },
            content: {
              type: 'string',
              description: 'Contenido del archivo'
            }
          },
          required: ['path', 'content']
        }
      },
      {
        name: 'onedrive_search',
        description: 'Busca archivos en OneDrive por nombre o contenido.',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Término de búsqueda'
            }
          },
          required: ['query']
        }
      },
      {
        name: 'onedrive_reconstruct_conversations',
        description: 'Reconstruye conversaciones de exports de ChatGPT, Claude, Gemini, NotebookLM en formato unificado.',
        inputSchema: {
          type: 'object',
          properties: {
            source_path: {
              type: 'string',
              description: 'Ruta del archivo de export (JSON)'
            },
            ai_type: {
              type: 'string',
              enum: ['chatgpt', 'claude', 'gemini', 'notebooklm', 'antigravity', 'codex'],
              description: 'Tipo de IA origen'
            },
            output_path: {
              type: 'string',
              description: 'Ruta de salida para el archivo reconstruido'
            }
          },
          required: ['source_path', 'ai_type']
        }
      },
      {
        name: 'onedrive_create_corpus',
        description: 'Crea un corpus completo unificado de todas las conversaciones en OneDrive.',
        inputSchema: {
          type: 'object',
          properties: {
            source_paths: {
              type: 'array',
              items: { type: 'string' },
              description: 'Rutas de archivos a incluir en el corpus'
            },
            output_path: {
              type: 'string',
              description: 'Ruta del corpus unificado',
              default: '/Nexus/corpus_completo_onedrive.json'
            }
          },
          required: ['source_paths']
        }
      },
      {
        name: 'onedrive_sync_with_gdrive',
        description: 'Sincroniza corpus reconstruido con Google Drive para análisis unificado.',
        inputSchema: {
          type: 'object',
          properties: {
            onedrive_path: {
              type: 'string',
              description: 'Ruta del corpus en OneDrive'
            },
            sync_mode: {
              type: 'string',
              enum: ['export_metadata', 'full_copy', 'incremental'],
              description: 'Modo de sincronización',
              default: 'export_metadata'
            }
          },
          required: ['onedrive_path']
        }
      }
    ]
  };
});

/**
 * MANEJADOR DE HERRAMIENTAS
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    // Asegurar que el cliente está inicializado
    if (!graphClient) {
      await initGraphClient();
    }

    switch (name) {
      case 'onedrive_list_files': {
        const path = args.path || NEXUS_WORKSPACE;
        const endpoint = path === '/' ?
          '/me/drive/root/children' :
          `/me/drive/root:${path}:/children`;

        const response = await graphClient.api(endpoint).get();

        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              path: path,
              entries: response.value.map(item => ({
                name: item.name,
                path: item.parentReference.path + '/' + item.name,
                type: item.folder ? 'folder' : 'file',
                size: item.size,
                modified: item.lastModifiedDateTime,
                id: item.id
              }))
            }, null, 2)
          }]
        };
      }

      case 'onedrive_read_file': {
        const endpoint = `/me/drive/root:${args.path}:/content`;
        const stream = await graphClient.api(endpoint).getStream();

        // Convertir stream a string
        const chunks = [];
        for await (const chunk of stream) {
          chunks.push(chunk);
        }
        const content = Buffer.concat(chunks).toString('utf-8');

        return {
          content: [{
            type: 'text',
            text: content
          }]
        };
      }

      case 'onedrive_write_file': {
        const content = Buffer.from(args.content, 'utf-8');
        const endpoint = `/me/drive/root:${args.path}:/content`;

        await graphClient.api(endpoint).put(content);

        return {
          content: [{
            type: 'text',
            text: `✅ Archivo escrito: ${args.path}`
          }]
        };
      }

      case 'onedrive_search': {
        const response = await graphClient
          .api('/me/drive/root/search(q=\'{query}\')')
          .get({ query: args.query });

        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              query: args.query,
              matches: response.value.map(item => ({
                name: item.name,
                path: item.parentReference.path + '/' + item.name,
                type: item.folder ? 'folder' : 'file',
                size: item.size
              }))
            }, null, 2)
          }]
        };
      }

      case 'onedrive_reconstruct_conversations': {
        // Leer archivo fuente
        const endpoint = `/me/drive/root:${args.source_path}:/content`;
        const stream = await graphClient.api(endpoint).getStream();

        const chunks = [];
        for await (const chunk of stream) {
          chunks.push(chunk);
        }
        const sourceContent = Buffer.concat(chunks).toString('utf-8');
        let sourceData;

        try {
          sourceData = JSON.parse(sourceContent);
        } catch (e) {
          return {
            content: [{
              type: 'text',
              text: `❌ Error: El archivo no es JSON válido`
            }],
            isError: true
          };
        }

        // Reconstruir según tipo de IA
        const reconstructed = await reconstructConversation(sourceData, args.ai_type);

        // Guardar reconstrucción
        const outputPath = args.output_path ||
          args.source_path.replace(/\.(json|txt)$/, '_reconstructed.json');

        const outputContent = Buffer.from(JSON.stringify(reconstructed, null, 2), 'utf-8');
        const outputEndpoint = `/me/drive/root:${outputPath}:/content`;
        await graphClient.api(outputEndpoint).put(outputContent);

        return {
          content: [{
            type: 'text',
            text: `✅ Conversación reconstruida:\n` +
                  `- Tipo: ${args.ai_type}\n` +
                  `- Mensajes: ${reconstructed.messages.length}\n` +
                  `- Guardado en: ${outputPath}`
          }]
        };
      }

      case 'onedrive_create_corpus': {
        const allConversations = [];

        for (const path of args.source_paths) {
          const endpoint = `/me/drive/root:${path}:/content`;
          const stream = await graphClient.api(endpoint).getStream();

          const chunks = [];
          for await (const chunk of stream) {
            chunks.push(chunk);
          }
          const content = JSON.parse(Buffer.concat(chunks).toString('utf-8'));
          allConversations.push(content);
        }

        const corpus = {
          version: '1.0.0',
          created: new Date().toISOString(),
          source: 'onedrive',
          total_conversations: allConversations.length,
          total_messages: allConversations.reduce((sum, conv) =>
            sum + (conv.messages?.length || 0), 0),
          conversations: allConversations
        };

        const corpusContent = Buffer.from(JSON.stringify(corpus, null, 2), 'utf-8');
        const outputEndpoint = `/me/drive/root:${args.output_path}:/content`;
        await graphClient.api(outputEndpoint).put(corpusContent);

        return {
          content: [{
            type: 'text',
            text: `✅ Corpus creado:\n` +
                  `- Conversaciones: ${corpus.total_conversations}\n` +
                  `- Mensajes totales: ${corpus.total_messages}\n` +
                  `- Guardado en: ${args.output_path}`
          }]
        };
      }

      case 'onedrive_sync_with_gdrive': {
        // Lee el corpus de OneDrive
        const endpoint = `/me/drive/root:${args.onedrive_path}:/content`;
        const stream = await graphClient.api(endpoint).getStream();

        const chunks = [];
        for await (const chunk of stream) {
          chunks.push(chunk);
        }
        const corpus = JSON.parse(Buffer.concat(chunks).toString('utf-8'));

        // Crear metadata para sincronización
        const syncMetadata = {
          sync_id: `onedrive_sync_${Date.now()}`,
          timestamp: new Date().toISOString(),
          source: 'onedrive',
          destination: 'google_drive',
          mode: args.sync_mode,
          corpus_stats: {
            total_conversations: corpus.total_conversations,
            total_messages: corpus.total_messages,
            size_bytes: Buffer.byteLength(JSON.stringify(corpus))
          },
          ready_for_claude_analysis: true
        };

        return {
          content: [{
            type: 'text',
            text: `✅ Metadata de sincronización preparada:\n${JSON.stringify(syncMetadata, null, 2)}\n\n` +
                  `📝 SIGUIENTE PASO: Usa el servidor MCP de Google Drive para importar este corpus.`
          }]
        };
      }

      default:
        return {
          content: [{
            type: 'text',
            text: `❌ Herramienta desconocida: ${name}`
          }],
          isError: true
        };
    }
  } catch (error) {
    return {
      content: [{
        type: 'text',
        text: `❌ Error: ${error.message}\n${error.stack}`
      }],
      isError: true
    };
  }
});

/**
 * FUNCIÓN DE RECONSTRUCCIÓN (idéntica a Dropbox para consistencia)
 */
async function reconstructConversation(data, aiType) {
  const reconstructed = {
    metadata: {
      ai_type: aiType,
      reconstructed_at: new Date().toISOString(),
      source: 'onedrive'
    },
    messages: []
  };

  switch (aiType) {
    case 'chatgpt':
      // ChatGPT export format
      for (const conv of (data.conversations || [])) {
        for (const node of Object.values(conv.mapping || {})) {
          if (node.message && node.message.content) {
            reconstructed.messages.push({
              role: node.message.author?.role || 'unknown',
              content: node.message.content.parts?.join('\n') || '',
              timestamp: node.message.create_time,
              id: node.message.id
            });
          }
        }
      }
      break;

    case 'claude':
      // Claude export format
      for (const msg of (data.messages || data.chat_messages || [])) {
        reconstructed.messages.push({
          role: msg.sender || msg.role,
          content: msg.text || msg.content,
          timestamp: msg.created_at || msg.timestamp,
          id: msg.uuid || msg.id
        });
      }
      break;

    case 'gemini':
      // Gemini export format
      for (const turn of (data.turns || [])) {
        reconstructed.messages.push({
          role: turn.role || 'user',
          content: turn.parts?.map(p => p.text).join('\n') || '',
          timestamp: turn.timestamp,
          id: turn.id
        });
      }
      break;

    case 'notebooklm':
      // NotebookLM format
      for (const entry of (data.entries || [])) {
        reconstructed.messages.push({
          role: 'user',
          content: entry.query || '',
          timestamp: entry.created,
          id: entry.id
        });
        if (entry.response) {
          reconstructed.messages.push({
            role: 'assistant',
            content: entry.response,
            timestamp: entry.created,
            id: entry.id + '_response'
          });
        }
      }
      break;

    case 'antigravity':
      // Antigravity format (Claude Code custom)
      for (const msg of (data.messages || [])) {
        reconstructed.messages.push({
          role: msg.role || 'user',
          content: msg.content,
          timestamp: msg.timestamp,
          id: msg.id,
          tools_used: msg.tools_used || []
        });
      }
      break;

    case 'codex':
      // OpenAI Codex format
      for (const completion of (data.completions || [])) {
        reconstructed.messages.push({
          role: 'user',
          content: completion.prompt,
          timestamp: completion.created,
          id: completion.id
        });
        reconstructed.messages.push({
          role: 'assistant',
          content: completion.choices[0]?.text || '',
          timestamp: completion.created,
          id: completion.id + '_response'
        });
      }
      break;

    default:
      // Generic format
      reconstructed.messages = data.messages || [];
  }

  return reconstructed;
}

/**
 * RECURSOS DISPONIBLES
 */
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: 'onedrive://workspace',
        name: 'Nexus Workspace',
        description: 'Workspace principal de Nexus en OneDrive',
        mimeType: 'application/json'
      }
    ]
  };
});

/**
 * INICIAR SERVIDOR
 */
async function main() {
  await initGraphClient();
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('🔱 Nexus OneDrive MCP Server iniciado');
}

main().catch((error) => {
  console.error('❌ Error fatal:', error);
  process.exit(1);
});
