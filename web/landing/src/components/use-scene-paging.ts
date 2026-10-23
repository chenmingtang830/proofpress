import { useEffect } from "react";

/** Native, gentle chapter settling; never intercept wheel, touch or keyboard input. */
export function useScenePaging() {
  useEffect(() => {
    document.documentElement.classList.add("sceneSnap");
    return () => document.documentElement.classList.remove("sceneSnap");
  }, []);
}
