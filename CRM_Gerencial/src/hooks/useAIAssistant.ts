import { useState, useCallback } from 'react';

interface AIResponse {
  success: boolean;
  message: string;
  data?: any;
  error?: string;
}

/**
 * Hook Premium: useAIAssistant
 * Permite a cualquier componente frontend interactuar con Bones (la IA de Axyntrax)
 * para inyectar datos del rubro, reestructurar vistas o solicitar análisis.
 */
export const useAIAssistant = (clientIndustry: string = 'general') => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [lastResponse, setLastResponse] = useState<AIResponse | null>(null);

  const requestAIAction = useCallback(async (action: string, payload: any) => {
    setIsProcessing(true);
    try {
      const response = await fetch('/api/ai-integration', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action,
          payload,
          clientIndustry,
        }),
      });

      const data: AIResponse = await response.json();
      setLastResponse(data);
      return data;
    } catch (error: any) {
      const errorData = { success: false, message: 'Error de red con la IA', error: error.message };
      setLastResponse(errorData);
      return errorData;
    } finally {
      setIsProcessing(false);
    }
  }, [clientIndustry]);

  const injectIndustryData = useCallback((schemaData: any) => {
    return requestAIAction('inject_data', schemaData);
  }, [requestAIAction]);

  const registerModule = useCallback((moduleDefinition: any) => {
    return requestAIAction('register_plugin', moduleDefinition);
  }, [requestAIAction]);

  return {
    isProcessing,
    lastResponse,
    injectIndustryData,
    registerModule,
    requestAIAction
  };
};
