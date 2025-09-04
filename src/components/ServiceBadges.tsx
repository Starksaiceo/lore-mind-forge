import { Badge } from '@/components/ui/badge';
import { Shield, AlertTriangle, XCircle } from 'lucide-react';
import type { IntegrationsStatus, ServiceState } from '@/lib/api';

interface ServiceBadgesProps {
  status: IntegrationsStatus;
}

function ServiceBadge({ name, state }: { name: string; state: ServiceState }) {
  const getVariant = () => {
    if (state.live && state.reason === 'ok') return 'success';
    if (state.live && state.reason === 'simulated') return 'warning';
    return 'error';
  };

  const getIcon = () => {
    if (state.live && state.reason === 'ok') return <Shield className="h-3 w-3" />;
    if (state.live && state.reason === 'simulated') return <AlertTriangle className="h-3 w-3" />;
    return <XCircle className="h-3 w-3" />;
  };

  const getText = () => {
    if (state.live && state.reason === 'ok') return `${name} Live`;
    if (state.live && state.reason === 'simulated') return `${name} Simulated`;
    return `${name} Down`;
  };

  return (
    <Badge variant={getVariant()} className="gap-1">
      {getIcon()}
      {getText()}
    </Badge>
  );
}

export default function ServiceBadges({ status }: ServiceBadgesProps) {
  return (
    <div className="flex flex-wrap gap-2">
      <ServiceBadge name="Stripe" state={status.stripe} />
      <ServiceBadge name="Shopify" state={status.shopify} />
      <ServiceBadge name="LLM" state={status.llm} />
      <ServiceBadge name="Meta Ads" state={status.meta_ads} />
      <ServiceBadge name="Google Ads" state={status.google_ads} />
      <ServiceBadge name="Policy" state={status.policy} />
      {status.github && <ServiceBadge name="GitHub" state={status.github} />}
    </div>
  );
}