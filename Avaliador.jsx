import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";

function gerarProdutoAleatorio() {
  const marcas = ["Nike", "Adidas", "Samsung", "Apple", "Coca-Cola", "Nestlé", "Pantene"];
  const tipos = ["Tênis", "Camiseta", "Shampoo", "Celular", "Chocolate", "Relógio", "Fone de Ouvido"];
  const marca = marcas[Math.floor(Math.random() * marcas.length)];
  const tipo = tipos[Math.floor(Math.random() * tipos.length)];
  const nome = `${tipo} ${marca}`;
  const imagem = `https://loremflickr.com/300/200/${encodeURIComponent(tipo)}`;
  return { id: Date.now(), nome, imagem };
}

export default function Avaliador() {
  const [produtoAtual, setProdutoAtual] = useState(null);
  const [saldo, setSaldo] = useState(0);
  const [avaliacoes, setAvaliacoes] = useState([]);
  const audioRef = useRef(null);

  const valorPorAvaliacao = 0.25;

  useEffect(() => {
    setProdutoAtual(gerarProdutoAleatorio());
  }, []);

  const avaliar = (resposta) => {
    setAvaliacoes([...avaliacoes, { id: produtoAtual.id, resposta }]);
    setSaldo((prev) => parseFloat((prev + valorPorAvaliacao).toFixed(2)));
    setProdutoAtual(gerarProdutoAleatorio());
    if (audioRef.current) {
      audioRef.current.currentTime = 0;
      audioRef.current.play();
    }
  };

  return (
    <div style={{ textAlign: 'center', padding: 20 }}>
      <audio ref={audioRef} src='/coin.mp3' preload='auto' />
      <h1 style={{ fontSize: 32, marginBottom: 10 }}>Avalie e ganhe 💸</h1>
      <p style={{ fontSize: 18 }}>Saldo acumulado: <strong>${saldo.toFixed(2)}</strong></p>
      <AnimatePresence mode='wait'>
        {produtoAtual && (
          <motion.div
            key={produtoAtual.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4 }}
            style={{
              maxWidth: 400,
              margin: '20px auto',
              background: '#fff',
              borderRadius: 16,
              boxShadow: '0 0 20px rgba(0,0,0,0.1)',
              padding: 20
            }}
          >
            <img src={produtoAtual.imagem} alt={produtoAtual.nome} style={{ width: '100%', borderRadius: 12 }} />
            <h2 style={{ margin: '16px 0' }}>{produtoAtual.nome}</h2>
            <div style={{ display: 'flex', justifyContent: 'center', gap: 10 }}>
              <button onClick={() => avaliar('usaria')}>✅ Usaria</button>
              <button onClick={() => avaliar('nao_usaria')}>❌ Não usaria</button>
              <button onClick={() => avaliar('talvez')}>🤔 Talvez</button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
