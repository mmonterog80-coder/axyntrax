"use client";
import { createContext, useContext } from "react";
import { motion, useReducedMotion } from "framer-motion";
const FadeInStaggerContext = createContext(false);

const viewport = { once: true, margin: "0px 0px -200px" };

const FadeIn = (props) => {
  const shouldReduceMotion = useReducedMotion();
  const isInStaggerGroup = useContext(FadeInStaggerContext);
  return (
    <motion.div
      variants={{
        hidden: { 
          opacity: 0, 
          y: shouldReduceMotion ? 0 : 30,
          scale: shouldReduceMotion ? 1 : 0.95,
          filter: shouldReduceMotion ? "blur(0px)" : "blur(8px)"
        },
        visible: { 
          opacity: 1, 
          y: 0,
          scale: 1,
          filter: "blur(0px)"
        },
      }}
      transition={{ duration: 0.8, ease: [0.21, 0.47, 0.32, 0.98] }}
      {...(isInStaggerGroup
        ? {}
        : {
            initial: "hidden",
            whileInView: "visible",
            viewport,
          })}
      {...props}
    />
  );
};

export const FadeInStagger = ({ faster = false, ...props  }: any) => {
  return (
    <FadeInStaggerContext.Provider value={true}>
      <motion.div
        initial="hidden"
        whileInView="visible"
        viewport={viewport}
        transition={{ staggerChildren: faster ? 0.12 : 0.2 }}
        {...props}
      />
    </FadeInStaggerContext.Provider>
  );
};

export default FadeIn;

