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
      <Elem name="heidi" tag="img" src={absoluteURL("/static/images/opossum_looking.png")} />
      <Elem name="header" tag="h1">Heidi doesn’t see any schs here</Elem>
      <p>Create one</p>
      <Elem name="action" tag={Button} onClick={openModal} look="primary">Create Schedule</Elem>
    </Block>
  );
};

export const PeopleList = ({ onSelect, selectedUser, defaultSelected }) => {
  const api = useAPI();
  const [schsList, setSchsList] = useState([]);
  const [currentPage, setCurrentPage] = useState(getCurrentPage());
  const [networkState, setNetworkState] = React.useState(null);
  const [currentPageSize] = usePageSize('page_size', 30);
  const [totalItems, setTotalItems] = useState(0);
  const [modal, setModal] = React.useState(false);
  const openModal = setModal.bind(null, true);
  const closeModal = setModal.bind(null, false);

  const setContextProps = useContextProps();
  const defaultPageSize = parseInt(localStorage.getItem('pages:projects-list') ?? 30);


  console.log({ currentPage, currentPageSize });

  const fetchSchs = useCallback(async (page= currentPage, pageSize= defaultPageSize) => {
    setNetworkState('loading');
    const response = await api.callApi('schs', {
      params: {
        page,
        page_size: pageSize,
      },
    });

    console.log(response.results ?? 1)
    setSchsList(response.results ?? []);
    setTotalItems(response.count);
    setNetworkState('loaded');
  }, [api]);

  const loadNextPage = async (page, pageSize) => {
    setCurrentPage(page);
    await fetchSchs(page, pageSize);
  };

  React.useEffect(() => {
    fetchSchs();
  }, []);

  React.useEffect(() => {
    // there is a nice page with Create button when list is empty
    // so don't show the context button in that case
    setContextProps({ openModal, showButton: schsList.length > 0 });
  }, [schsList.length]);


  useEffect(() => {
    if (isDefined(defaultSelected) && schsList) {
      const selected = schsList.find(({ user }) => user.id === Number(defaultSelected));

      if (selected) selectUser(selected.user);
    }
  }, [schsList, defaultSelected]);

  return (
    <>
      <Block name="sch-list">
        <Oneof value={networkState}>
          <Elem name="loading" case="loading">
            <Spinner size={64}/>
          </Elem>
          <Elem name="wrapper" case="loaded">
              {schsList ? (
                <Elem name="schs">
                  <Elem name="header">
                    <Elem name="column" mix="avatar"/>
                    <Elem name="column" mix="title">Name</Elem>
                    <Elem name="column" mix="dataset">Dataset</Elem>
                    <Elem name="column" mix="created-by">Created By</Elem>
                  </Elem>
                  <Elem name="body">
                    {schsList.map(({ sch }) => {
                      const active = sch.id === selectedUser?.id;

                      return (
                        <Elem key={`sch-${sch.id}`} name="sch" mod={{ active }} onClick={() => selectUser(sch)}>
                          <Elem name="field" mix="avatar">
                            <Userpic sch={sch} style={{ width: 28, height: 28 }}/>
                          </Elem>
                          <Elem name="field" mix="title">
                            {sch.title}
                          </Elem>
                          <Elem name="field" mix="dataset">
                            {sch.dataset}
                          </Elem>
                          <Elem name="field" mix="created-by">
                            {sch.created_by_id}
                          </Elem>
                        </Elem>
                      );
                    })}
                  </Elem>
                </Elem>
              ) : (
                <Elem name="loading">
                  {/* <Spinner size={36}/> */}
                  <EmptySchsList openModal={openModal} />
                </Elem>
              )}
              {modal && <CreateSch onClose={closeModal} />}
            </Elem>
          <Pagination
            page={currentPage}
            urlParamName="page"
            totalItems={totalItems}
            pageSize={currentPageSize}
            pageSizeOptions={[30, 50, 100]}
            onPageLoad={fetchSchs}
            style={{ paddingTop: 16 }}
          />
        </Oneof>
      </Block>
    </>
  );
};
