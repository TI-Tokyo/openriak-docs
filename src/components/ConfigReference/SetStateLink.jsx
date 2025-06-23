export default function SetStateLink({linkText, setValue, setMethod, className}) {
  //console.log(linkText);
  //console.log(setValue);
  //console.log(setMethod);
  const handleClick = (event) => {
    event.preventDefault();
    setMethod(setValue);
  };

  return (
    <a href="#" className={className} onClick={handleClick}>{linkText}</a>
  );
}
