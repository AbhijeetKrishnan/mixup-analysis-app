function onSubmit(e: Event) {
  e.preventDefault(); // prevent the default form submission behavior
  const form = e.target as HTMLFormElement; // cast the target to HTMLFormElement
  const formData = new FormData(form);
  const data = Object.fromEntries(formData); // use the form to create a new FormData object

  console.log(data);
}