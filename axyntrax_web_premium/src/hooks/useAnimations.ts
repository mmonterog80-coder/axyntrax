export function useFadeInVariants() {
  return {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.8, ease: "easeOut" },
  };
}

export function useStaggerVariants() {
  return {
    initial: "initial",
    animate: "animate",
    variants: {
      initial: {},
      animate: {
        transition: { staggerChildren: 0.2 },
      },
    },
  };
}
