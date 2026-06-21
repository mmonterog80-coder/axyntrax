import ContactSection from "@/components/ContactSection";
import Container from "@/components/Container";
import Cultures from "@/components/Cultures";
import PageIntro from "@/components/PageIntro";
import { StatList, StatListItem } from "@/components/StatList";
import React from "react";

const AboutPage = () => {
  return (
    <>
      <PageIntro eyebrow="Nosotros" title="Nuestra fuerza es la innovación">
        <p>
          Creemos que el éxito de nuestros clientes es nuestro propio éxito. Proveemos
          la tecnología que transforma negocios tradicionales en líderes del mercado.
        </p>
        <div className="mt-10 max-w-2xl space-y-6 text-base">
          <p>
            Axyntrax nació con la misión de democratizar el software empresarial de alto rendimiento.
            Sabemos que industrias como la Veterinaria, Dental, Bodega, Restaurantes y Talleres 
            necesitan soluciones integrales, rápidas y seguras.
          </p>
          <p>
            En Axyntrax, combinamos diseño premium con ingeniería de primer nivel para ofrecerte 
            módulos intuitivos que tus equipos amarán usar día a día, eliminando cuellos de botella 
            y potenciando tu rentabilidad.
          </p>
        </div>
      </PageIntro>
      <Container className="mt-16">
        <StatList>
          <StatListItem value="150+" label="Clientes activos" />
          <StatListItem value="6" label="Módulos especializados" />
          <StatListItem value="99.9%" label="Uptime garantizado" />
        </StatList>
      </Container>
      <Cultures />
      <ContactSection />
    </>
  );
};

export default AboutPage;
