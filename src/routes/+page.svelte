<script>
  let brukere = "";

  async function hent_data() {
    const respons = await fetch("http://127.0.0.1:5000/");
    const data = await respons.json();
    brukere = data.brukere;
  }
</script>

<button on:click={hent_data}>Hent data</button>
<p>{brukere}</p>

<a href="/innlogging">Logg inn</a>
<br />
<a href="/registrering">Registrer deg</a>
