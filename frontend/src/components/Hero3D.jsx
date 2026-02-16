import { Canvas } from "@react-three/fiber";

export default function Hero3D() {
  return (
    <Canvas camera={{ position: [0,0,5] }}>
      <ambientLight intensity={0.6} />
      <mesh rotation={[0.4,0.3,0]}>
        <boxGeometry args={[2,2,2]} />
        <meshStandardMaterial color="#2563eb" />
      </mesh>
    </Canvas>
  );
}
