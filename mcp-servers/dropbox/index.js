#!/usr/bin/env node

/**
 * 🔱 NEXUS MCP SERVER - DROPBOX
 * Servidor MCP para acceso a Dropbox con capacidades de reconstrucción de conversaciones
 * Diseñado para integrarse con Claude Desktop y procesar exports de IAs
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { Dropbox } from 'dropbox';
import fetch from 'node-fetch';
import * as dotenv from 'dotenv';

dotenv.config();

// Configuración
const DROPBOX_ACCESS_TOKEN = process.env.DROPBOX_ACCESS_TOKEN;
const NEXUS_WORKSPACE = process.env.NEXUS_WORKSPACE || '/Nexus';

if (!DROPBOX_ACCESS_TOKEN) {
  console.error('❌ ERROR: DROPBOX_ACCESS_TOKEN no configurado en .env');
  process.exit(1);
}

// Inicializar cliente Dropbox
const dbx = new Dropbox({
  accessToken: DROPBOX_ACCESS_TOKEN,
  fetch: fetch
});

// Inicializar servidor MCP
const server = new Server(
  {
    name: 'nexus-dropbox-server',
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
        name: 'dropbox_list_files',
        description: 'Lista archivos y carpetas en Dropbox. Útil para explorar exports de conversaciones.',
        inputSchema: {
          type: 'object',
          properties: {
            path: {
              type: 'string',
              description: 'Ruta en Dropbox (por defecto: /Nexus)',
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
        name: 'dropbox_read_file',
        description: 'Lee contenido de un archivo en Dropbox. Soporta JSON, TXT, MD, HTML.',
        inputSchema: {
          type: 'object',
          properties: {
            path: {
              type: 'string',
              description: 'Ruta completa del archivo en Dropbox'
            }
          },
          required: ['path']
        }
      },
      {
        name: 'dropbox_write_file',
        description: 'Escribe o actualiza un archivo en Dropbox.',
        inputSchema: {
          type: 'object',
          properties: {
            path: {
              type: 'string',
              description: 'Ruta completa del archivo en Dropbox'
            },
            content: {
              type: 'string',
              description: 'Contenido del archivo'
            },
            mode: {
              type: 'string',
              enum: ['add', 'overwrite', 'update'],
              description: 'Modo de escritura',
              default: 'add'
            }
          },
          required: ['path', 'content']
        }
      },
      {
        name: 'dropbox_search',
        description: 'Busca archivos en Dropbox por nombre o contenido.',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Término de búsqueda'
            },
            path: {
              type: 'string',
              description: 'Ruta donde buscar',
              default: NEXUS_WORKSPACE
            }
          },
          required: ['query']
        }
      },
      {
        name: 'dropbox_reconstruct_conversations',
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
        name: 'dropbox_create_corpus',
        description: 'Crea un corpus completo unificado de todas las conversaciones en Dropbox.',
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
              default: '/Nexus/corpus_completo_dropbox.json'
            }
          },
          required: ['source_paths']
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
    switch (name) {
      case 'dropbox_list_files': {
        const path = args.path || NEXUS_WORKSPACE;
        const result = await dbx.filesListFolder({ path });

        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              path: path,
              entries: result.result.entries.map(entry => ({
                name: entry.name,
                path_display: entry.path_display,
                type: entry['.tag'],
                size: entry.size,
                modified: entry.server_modified
              })),
              has_more: result.result.has_more
            }, null, 2)
          }]
        };
      }

      case 'dropbox_read_file': {
        const response = await dbx.filesDownload({ path: args.path });
        const content = response.result.fileBinary.toString('utf-8');

        return {
          content: [{
            type: 'text',
            text: content
          }]
        };
      }

      case 'dropbox_write_file': {
        const content = Buffer.from(args.content, 'utf-8');
        const mode = args.mode || 'add';

        const result = await dbx.filesUpload({
          path: args.path,
          contents: content,
          mode: mode === 'overwrite' ? { '.tag': 'overwrite' } : { '.tag': 'add' }
        });

        return {
          content: [{
            type: 'text',
            text: `✅ Archivo escrito: ${result.result.name} (${result.result.size} bytes)`
          }]
        };
      }

      case 'dropbox_search': {
        const searchPath = args.path || NEXUS_WORKSPACE;
        const result = await dbx.filesSearchV2({
          query: args.query,
          options: {
            path: searchPath,
            max_results: 100
          }
        });

        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              query: args.query,
              matches: result.result.matches.map(match => ({
                path: match.metadata.metadata.path_display,
                name: match.metadata.metadata.name,
                type: match.metadata.metadata['.tag']
              }))
            }, null, 2)
          }]
        };
      }

      case 'dropbox_reconstruct_conversations': {
        // Leer archivo fuente
        const sourceFile = await dbx.filesDownload({ path: args.source_path });
        const sourceContent = sourceFile.result.fileBinary.toString('utf-8');
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
        await dbx.filesUpload({
          path: outputPath,
          contents: outputContent,
          mode: { '.tag': 'overwrite' }
        });

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

      case 'dropbox_create_corpus': {
        const allConversations = [];

        for (const path of args.source_paths) {
          const file = await dbx.filesDownload({ path });
          const content = JSON.parse(file.result.fileBinary.toString('utf-8'));
          allConversations.push(content);
        }

        const corpus = {
          version: '1.0.0',
          created: new Date().toISOString(),
          source: 'dropbox',
          total_conversations: allConversations.length,
          total_messages: allConversations.reduce((sum, conv) =>
            sum + (conv.messages?.length || 0), 0),
          conversations: allConversations
        };

        const corpusContent = Buffer.from(JSON.stringify(corpus, null, 2), 'utf-8');
        await dbx.filesUpload({
          path: args.output_path,
          contents: corpusContent,
          mode: { '.tag': 'overwrite' }
        });

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
        text: `❌ Error: ${error.message}`
      }],
      isError: true
    };
  }
});

/**
 * FUNCIÓN DE RECONSTRUCCIÓN
 */
async function reconstructConversation(data, aiType) {
  const reconstructed = {
    metadata: {
      ai_type: aiType,
      reconstructed_at: new Date().toISOString(),
      source: 'dropbox'
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
        uri: 'dropbox://workspace',
        name: 'Nexus Workspace',
        description: 'Workspace principal de Nexus en Dropbox',
        mimeType: 'application/json'
      }
    ]
  };
});

/**
 * INICIAR SERVIDOR
 */
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('🔱 Nexus Dropbox MCP Server iniciado');
}

main().catch((error) => {
  console.error('❌ Error fatal:', error);
  process.exit(1);
});
