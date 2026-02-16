import { Canvas } from "@react-three/fiber";

export default function Hero3D() {
  return (
    <div className="hero">
      <Canvas>
        <ambientLight />
        <mesh rotation={[0.4,0.3,0]}>
          <boxGeometry args={[2,2,2]} />
          <meshStandardMaterial color="#2563eb" />
        </mesh>
      </Canvas>
    </div>
  );
}
