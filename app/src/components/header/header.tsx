"use client";
import { Bars3Icon } from '@heroicons/react/24/solid';
import Link from 'next/link';
import ThemeToggle from '../theme-toggle/theme-toggle';

const renderMenuItems = () => {
  return (
    <>
      <li>
        <Link href="/" data-testid="home">
          Home
        </Link>
      </li>
      <li>
        <Link href="/well-architected" data-testid="well-architected">
          Azure Well-Architected
        </Link>
      </li>
      <li>
        <details>
          <summary>Azure Docs</summary>
          <ul className="p-2">
            <li><Link href="/docs/submenu1">Submenu 1</Link></li>
            <li><Link href="/docs/submenu2">Submenu 2</Link></li>
          </ul>
        </details>
      </li>
      <li>
        <ThemeToggle />
      </li>
    </>
  )
}

export const Header = () => {

  return (
    <div id="header" data-testid="header" className="navbar bg-base-100 mx-auto shadow-sm">
      <div className="navbar-start">
        <div className="dropdown">
          <button tabIndex={0} data-testid="dropdown-button" className="btn btn-ghost lg:hidden">
            <Bars3Icon className="h-5 w-5" />
          </button>
          <ul className="menu menu-sm dropdown-content bg-base-100 rounded-box z-1 mt-3 w-52 p-2 shadow">
            {renderMenuItems()}
          </ul>
        </div>
        <a className="btn btn-ghost text-xl">Azure Mind Map</a>
      </div>
      <div className="navbar-end hidden lg:flex">
        <ul id="navbar-menu" data-testid="navbar-menu" className="menu menu-horizontal px-1">
          {renderMenuItems()}
        </ul>
      </div>
    </div>
  );
}
