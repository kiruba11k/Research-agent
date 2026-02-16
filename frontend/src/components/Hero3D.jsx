import { useFrame } from "@react-three/fiber";
import { useRef } from "react";

export default function Hero3D() {
  const meshRef = useRef();

  // Optimized animation loop running outside React's render cycle
  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.5;
      meshRef.current.rotation.x += delta * 0.2;
    }
  });

  return (
    <mesh ref={meshRef} rotation={[0.4, 0.3, 0]}>
      <boxGeometry args={[2, 2, 2]} />
      <meshDistortMaterial color="#2563eb" speed={2} distort={0.4} />
    </mesh>
  );
}
