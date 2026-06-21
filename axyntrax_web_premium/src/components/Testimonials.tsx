import React from "react";
import GridPattern from "./GridPattern";
import clsx from "clsx";
import Container from "./Container";
import FadeIn from "./FadeIn";
import Image from "next/image";
import { motion } from "framer-motion";

const Testimonials = ({ children, client, className  }: any) => {
  return (
    <div
      className={clsx(
        "relative isolate bg-neutral-50 py-16 sm:py-28 md:py-32",
        className
      )}
    >
      <GridPattern
        className="absolute inset-0 -z-10 h-full w-full fill-neutral-100 stroke-neutral-950/5 [mask-image:linear-gradient(to_bottom_left,white_50%,transparent_60%)]"
        yOffset={-256}
      />
      <Container>
        <FadeIn>
          <figure className="mx-auto max-w-4xl flex flex-col items-center text-center">
            <blockquote className="relative font-display text-3xl font-medium tracking-tight text-neutral-950 sm:text-4xl">
              <motion.p 
                initial={{ opacity: 0, rotateX: 90 }}
                whileInView={{ opacity: 1, rotateX: 0 }}
                transition={{ duration: 0.8, ease: "easeOut" }}
                viewport={{ once: true, margin: "-100px" }}
                className="before:content-['“'] after:content-['”'] sm:before:absolute sm:before:right-full"
              >
                {children}
              </motion.p>
            </blockquote>
            <figcaption className="mt-10">
              <motion.div
                initial={{ opacity: 0, scale: 0.8, filter: "grayscale(100%)" }}
                whileInView={{ opacity: 1, scale: 1, filter: "grayscale(0%)" }}
                transition={{ delay: 0.3, duration: 0.8 }}
                viewport={{ once: true }}
              >
                <Image src={client.logo} alt={client.name} unoptimized />
              </motion.div>
            </figcaption>
          </figure>
        </FadeIn>
      </Container>
    </div>
  );
};

export default Testimonials;
