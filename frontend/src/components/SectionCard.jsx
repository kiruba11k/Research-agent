export default function SectionCard({ title, data }) {
  return (
    <div>
      <h2>{title}</h2>
      <p>{data.content}</p>
      <p>Confidence: {Math.round(data.confidence * 100)}%</p>
    </div>
  );
}
