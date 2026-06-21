export function constructMetadata({
  title = "Axyntrax | Módulos Comerciales",
  description = "Axyntrax: Plataforma premium con módulos de Veterinaria, Dental, CRM, Bodega, Restaurante y Taller.",
  image = "/agency.PNG",
  icons = "/favicon.ico",
  noIndex = false,
}) {
  return {
    title,
    description,
    openGraph: {
      title,
      description,
      images: [
        {
          url: image,
        },
      ],
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [image],
      creator: "@Axyntrax",
    },
    icons,
    metadataBase: new URL("https://axyntrax.com/"),
    themeColor: "#050505",
    ...(noIndex && {
      robots: {
        index: false,
        follow: false,
      },
    }),
  };
}
