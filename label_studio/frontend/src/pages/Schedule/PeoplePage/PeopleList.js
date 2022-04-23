import { formatDistance } from "date-fns";
import React, { useCallback, useEffect, useState } from "react";
import { Pagination, Spinner, Userpic } from "../../../components";
import { usePage, usePageSize } from "../../../components/Pagination/Pagination";
import { useContextProps } from '../../../providers/RoutesProvider';
import { useAPI } from "../../../providers/ApiProvider";
import { Block, Elem } from "../../../utils/bem";
import { isDefined } from "../../../utils/helpers";
import { useUpdateEffect } from "../../../utils/hooks";
import { CreateSch } from "./CreateSch";
import { Button } from "../../../components";
import { absoluteURL } from '../../../utils/helpers';
import { Oneof } from '../../../components/Oneof/Oneof';
import './PeopleList.styl';

const getCurrentPage = () => {
  const pageNumberFromURL = new URLSearchParams(location.search).get("page");

  return pageNumberFromURL ? parseInt(pageNumberFromURL) : 1;
};

export const EmptySchsList = ({ openModal }) => {
  return (
    <Block name="empty-schs-page">
      <Elem name="header" tag="h1">Heidi doesn’t see any schs here</Elem>
      <p>Create one</p>
      <Elem name="action" tag={Button} onClick={openModal} look="primary">Create Schedule</Elem>
    </Block>
  );
};

export const PeopleList = ( { schsList }) => {
  // useEffect(() => {
  //   if (isDefined(defaultSelected) && schsList) {
  //     const selected = schsList.find(({ user }) => user.id === Number(defaultSelected));

  //     if (selected) selectUser(selected.user);
  //   }
  // }, [schsList, defaultSelected]);

  return (
    <>
      <Block name="sch-list">
        <Elem name="wrapper">
          <Elem name="schs">
            <Elem name="header">
              <Elem name="column" mix="title">Name</Elem>
              <Elem name="column" mix="dataset">Dataset</Elem>
              <Elem name="column" mix="created-by">Created By</Elem>
            </Elem>
            <Elem name="body">
              {schsList.map((sch) => {

                return (
                  <Elem key={`sch-${sch.id}`} name="sch">
                    <Elem name="field" mix="title">
                      {sch.title}
                    </Elem>
                    <Elem name="field" mix="dataset">
                      {sch.dataset}
                    </Elem>
                    <Elem name="field" mix="created-by">
                      {sch.created_by.email}
                    </Elem>
                  </Elem>
                )
              })}
            </Elem>
          </Elem>
        </Elem>
      </Block>
    </>
  );
};
