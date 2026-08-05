import React, {type ReactNode} from 'react';
import Link from '@docusaurus/Link';

import styles from './styles.module.css';

type Props = {
  compact?: boolean;
};

export default function AIContentNotice({compact = false}: Props): ReactNode {
  return (
    <aside
      className={styles.notice}
      role="note"
      aria-label="Aviso de contenido generado mediante inteligencia artificial">
      <div className={styles.badge}>IA · Generado</div>
      <div>
        <strong>Contenido generado por IA · Sin revisión humana</strong>
        {!compact && (
          <p>
            Este artículo forma parte de un experimento de publicación automatizada.
            Puede contener errores, omisiones o información desactualizada. Contrasta
            cualquier hallazgo importante con las fuentes originales.{' '}
            <Link to="/ai-experiment">Cómo funciona el experimento</Link>.
          </p>
        )}
      </div>
    </aside>
  );
}
