/**
 * PluginManager - Constructor de Ecosistemas
 * Arquitectura modular que permite a los módulos (plugins) acoplarse y desacoplarse 
 * dinámicamente sin afectar el "Core" del CRM.
 */
export class PluginManager {
  private static plugins: Map<string, any> = new Map();
  private static listeners: Map<string, Function[]> = new Map();

  /**
   * Registra un nuevo módulo provisto por la IA o un desarrollador
   */
  public static registerAIPlugin(pluginDefinition: any) {
    if (!pluginDefinition.name) {
      throw new Error("El plugin de IA debe tener un nombre válido.");
    }
    this.plugins.set(pluginDefinition.name, pluginDefinition);
    console.log(`[Ecosistema Next.js] Plugin registrado exitosamente: ${pluginDefinition.name}`);
    return { registered: true, pluginName: pluginDefinition.name };
  }

  /**
   * Permite que los módulos se comuniquen entre sí o con la IA mediante eventos
   */
  public static notifyEcosystem(event: string, data: any) {
    console.log(`[Ecosistema Evento] ${event} emitido.`);
    const eventListeners = this.listeners.get(event) || [];
    eventListeners.forEach(listener => listener(data));
  }

  /**
   * Suscribe el frontend o el CRM Core a eventos inyectados por la IA
   */
  public static subscribe(event: string, callback: Function) {
    const existing = this.listeners.get(event) || [];
    this.listeners.set(event, [...existing, callback]);
  }
}
