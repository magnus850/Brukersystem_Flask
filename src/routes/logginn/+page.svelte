<script>
  let resultat = "";
  let brukernavn = "";
  let passord = "";
  async function logg_inn() {
    const respons = await fetch("http://127.0.0.1:5000/");
    const data = await respons.json();
    resultat = data.resultat;
  }
  function print_input() {
    console.log(brukernavn);
    console.log(passord);
  }
</script>

<label for="brukernavn">Brukernavn:</label>
<input
  type="text"
  id="brukernavn"
  bind:value={brukernavn}
  on:blur={print_input}
/>
<br />
<label for="passord">Passord:</label>
<input type="text" id="passord" bind:value={passord} on:blur={print_input} />

<button on:click={logg_inn}>Logg inn</button>
