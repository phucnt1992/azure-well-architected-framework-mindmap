export const Footer = () => {
  const year = new Date().getFullYear();
  return (
    <footer id="footer" data-testid="footer" className="footer sm:footer-horizontal footer-center bg-base-300 text-base-content p-4" >
      <aside>
        <p>Copyright © {year} - Phuc Nguyen </p>
        <p>All rights reserved.</p>
      </aside>
    </footer>
  );
}
