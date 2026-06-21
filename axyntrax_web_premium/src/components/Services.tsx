import React from "react";
import SectionIntro from "./SectionIntro";
import Container from "./Container";
import FadeIn, { FadeInStagger } from "./FadeIn";
import StylizedImage from "./StylizedImage";
import imageLaptop from "../images/laptop.jpg";
import List, { ListItem } from "./List";

const Services = () => {
  return (
    <>
      <SectionIntro
        eyebrow="Soluciones"
        title="Diseñamos el ecosistema perfecto para tu industria."
        className="mt-24 sm:mt-32 lg:mt-40"
      >
        <p>
          En Axyntrax, cada producto es concebido con excelencia, garantizando la máxima productividad 
          para tu rubro específico a través de nuestra suite comercial integral.
        </p>
      </SectionIntro>
      <Container className="mt-16">
        <div className="lg:flex lg:items-center lg:justify-end">
          <div className="flex justify-center lg:w-1/2 lg:justify-end lg:pr-12">
            <FadeIn className="w-[33.75rem] flex-none lg:w-[45rem]">
              <StylizedImage
                src={imageLaptop}
                sizes="(min-width: 1024px) 41rem, 31rem"
                className="justify-center lg:justify-end"
              />
            </FadeIn>
          </div>
          {/* List item */}
          <List className="mt-16 lg:mt-0 lg:w-1/2 lg:min-w-[33rem] lg:pl-4">
            <ListItem title="Sistemas de Gestión Veterinaria y Dental">
              Administración eficiente de pacientes, historiales clínicos, y agendamiento 
              con una interfaz impecable que facilita el día a día de profesionales de la salud.
            </ListItem>
            <ListItem title="CRM Avanzado">
              Fideliza a tus clientes e incrementa tus ventas. Nuestro CRM te permite visualizar 
              embudos de conversión y automatizar el seguimiento con métricas en tiempo real.
            </ListItem>
            <ListItem title="Punto de Venta para Restaurantes">
              Gestión de mesas, toma de pedidos ágil, integración con cocina y facturación en 
              un sistema fluido y libre de interrupciones que tus empleados amarán.
            </ListItem>
            <ListItem title="Control de Inventario y Bodega">
              Mantén el control absoluto de tus existencias. Reportes automatizados, trazabilidad 
              y alertas de stock para optimizar la logística de tu empresa sin esfuerzo.
            </ListItem>
            <ListItem title="Administración de Taller">
              Órdenes de trabajo, inventario de repuestos, y estado de reparaciones centralizados 
              para que tu taller mecánico o de servicio funcione con total transparencia.
            </ListItem>
          </List>
        </div>
      </Container>
    </>
  );
};

export default Services;
