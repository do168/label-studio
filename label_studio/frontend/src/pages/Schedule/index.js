
import React from 'react';
import { SidebarMenu } from '../../components/SidebarMenu/SidebarMenu';
import { PeoplePage } from './PeoplePage/PeoplePage';
import { WebhookPage } from '../WebhookPage/WebhookPage';

const ALLOW_SCH_WEBHOOKS = window.APP_SETTINGS.flags?.allow_sch_webhooks;


const MenuLayout = ({ children, ...routeProps }) => {
  let menuItems = [PeoplePage];
  if (ALLOW_SCH_WEBHOOKS){
    menuItems.push(
      WebhookPage,
    );
  }
  return (
    <SidebarMenu
      menuItems={menuItems}
      path={routeProps.match.url}
      children={children}
    />
  );
};

const schPages = {};
if (ALLOW_SCH_WEBHOOKS){
  schPages[WebhookPage] = WebhookPage;
}

export const SchPage = {
  title: "Schs",
  path: "/sch",
  exact: true,
  layout: MenuLayout,
  component: PeoplePage,
  pages: schPages,
};
