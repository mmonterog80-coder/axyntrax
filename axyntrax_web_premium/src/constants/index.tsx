import { SocialMediaProfiles } from "@/components/SocialMedia";

export const navigation = [
  {
    title: "Soluciones",
    links: [
      { title: "Veterinaria", href: "/soluciones/veterinaria" },
      { title: "Dental", href: "/soluciones/dental" },
      { title: "CRM", href: "/soluciones/crm" },
      { title: "Restaurante", href: "/soluciones/restaurante" },
      { title: "Bodega", href: "/soluciones/bodega" },
      { title: "Taller", href: "/soluciones/taller" },
      {
        title: (
          <>
            Ver todo <span aria-hidden="true">&rarr;</span>
          </>
        ),
        href: "/soluciones",
      },
    ],
  },
  {
    title: "Compañía",
    links: [
      { title: "Nosotros", href: "/about" },
      { title: "Procesos", href: "/process" },
      { title: "Blog", href: "/blog" },
      { title: "Contacto", href: "/contact" },
    ],
  },
  {
    title: "Redes",
    links: SocialMediaProfiles,
  },
];
