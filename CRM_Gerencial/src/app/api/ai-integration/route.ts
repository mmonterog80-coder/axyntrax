import { NextResponse } from 'next/server';
import { AiInjector } from '@/modules/ai-bridge/AiInjector';
import { PluginManager } from '@/modules/core/PluginManager';

// Endpoint para que la IA integre datos o configuraciones según el rubro del cliente
export async function POST(request: Request) {
  try {
    const data = await request.json();
    const { action, payload, clientIndustry } = data;

    if (!action || !payload) {
      return NextResponse.json({ error: 'Faltan parámetros requeridos: action y payload' }, { status: 400 });
    }

    // Inicializar el inyector con el rubro del cliente, si existe
    const injector = new AiInjector(clientIndustry || 'general');

    let result;
    switch (action) {
      case 'inject_data':
        // Inyectar datos específicos (ej: configuración de BD o módulos)
        result = await injector.injectIndustryData(payload);
        break;
      
      case 'register_plugin':
        // Integración con el Constructor de Ecosistemas
        result = PluginManager.registerAIPlugin(payload);
        break;

      default:
        return NextResponse.json({ error: 'Acción no soportada por el puente de IA' }, { status: 400 });
    }

    return NextResponse.json({
      success: true,
      message: 'Operación ejecutada con éxito por la IA',
      data: result,
    });

  } catch (error: any) {
    console.error('Error en AI Integration API:', error);
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
