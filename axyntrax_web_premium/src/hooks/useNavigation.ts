import { useEffect, useState, useRef } from "react";

export function useNavigation() {
  const [expanded, setExpanded] = useState(false);
  const openRef = useRef<HTMLButtonElement>(null);
  const closeRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    function onClick(event: MouseEvent) {
      if ((event.target as Element).closest("a")?.href === window.location.href) {
        setExpanded(false);
      }
    }
    window.addEventListener("click", onClick);

    return () => {
      window.removeEventListener("click", onClick);
    };
  }, []);

  const toggleNavigation = () => {
    setExpanded((prev) => !prev);
    if (!expanded) {
      window.setTimeout(() => closeRef.current?.focus({ preventScroll: true }));
    } else {
      window.setTimeout(() => openRef.current?.focus({ preventScroll: true }));
    }
  };

  return { expanded, setExpanded, toggleNavigation, openRef, closeRef };
}
