const form = document.querySelector(".contact-form");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const nome = form.querySelector("input[placeholder='Seu nome']").value;
  const email = form.querySelector("input[placeholder='Seu email']").value;
  const mensagem = form.querySelector("textarea").value;

  try {
    const response = await fetch(
      "https://cafe-prosa-backend.onrender.com/contato",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ nome, email, mensagem })
      }
    );

    const data = await response.json();

    if (response.ok) {
      alert("Mensagem enviada com sucesso ☕💬");
      form.reset();
    } else {
      alert(data.erro || "Erro ao enviar mensagem");
    }
  } catch (err) {
    alert("Erro de conexão com o servidor");
  }
});
