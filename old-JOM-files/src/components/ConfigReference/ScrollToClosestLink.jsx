export default function ScrollToClosestLink({linkText, targetId, closestSelector}) {
  const handleClick = (event) => {
    event.preventDefault();

    const target = document.getElementById(targetId);
    const targetReal = target?.closest(closestSelector) ?? '';
    if (targetReal) {
      targetReal.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <a href="#" onClick={handleClick}>{linkText}</a>
  );
}
