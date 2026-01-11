const form = document.getElementById("contact-form");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const dados = {
    nome: document.getElementById("nome").value,
    email: document.getElementById("email").value,
    mensagem: document.getElementById("mensagem").value
  };

  const resposta = await fetch("http://127.0.0.1:5000/contato", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(dados)
  });

  const resultado = await resposta.json();
  alert(resultado.mensagem);

  form.reset();
});