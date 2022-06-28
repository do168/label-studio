import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useAPI } from "../../../providers/ApiProvider";
import { useConfig } from "../../../providers/ConfigProvider";
import { useContextProps } from '../../../providers/RoutesProvider';
import { Block, Elem } from "../../../utils/bem";
import "./PeopleInvitation.styl";
import { PeopleList, EmptySchsList } from "./PeopleList";
import "./PeoplePage.styl";
import { SelectedUser } from "./SelectedUser";
import { CreateSch } from "./CreateSch";
import { Space } from "../../../components/Space/Space";
import { Button } from "../../../components";
import { LsPlus } from "../../../assets/icons";
import React from "react";
import { Oneof } from '../../../components/Oneof/Oneof';
import { Pagination, Spinner, Userpic } from "../../../components";




export const PeoplePage = () => {

  const api = useAPI();
  const [schsList, setSchsList] = useState([]);
  const [networkState, setNetworkState] = React.useState(null);
  const [modal, setModal] = React.useState(false);
  const openModal = setModal.bind(null, true);
  const closeModal = setModal.bind(null, false);
  const [selectedScheduleList, setSelectedScheduleList] = React.useState([]);

  const setContextProps = useContextProps();


  const fetchSchs = async () => {
    setNetworkState('loading');
    const response = await api.callApi('schs', {
    });

    console.log("response.result: ", response)
    setSchsList(response ?? []);
    console.log(schsList);
    setNetworkState('loaded');
  };

  React.useEffect(() => {
    fetchSchs();
  }, []);

  React.useEffect(() => {
    // there is a nice page with Create button when list is empty
    // so don't show the context button in that case
    setContextProps({ openModal, showButton: schsList.length > 0 });
  }, [schsList.length]);


  const getSelectedRows = (selectedScheduleList) => {
    console.log(selectedScheduleList);
    setSelectedScheduleList(selectedScheduleList);
  }

  const deleteSchs = async() => {
    console.log(selectedScheduleList);
  }


  return (
    <Block name="people">
      <Elem name="controls">
        <Space spread>
          <Space></Space>

          <Space>
          <Elem tag={Button} onClick={deleteSchs}>Delete Schedule</Elem>
          <Elem name="action" tag={Button} onClick={openModal} look="primary">Create Schedule</Elem>
          </Space>
        </Space>
        {modal && <CreateSch onClose={closeModal} />}
      </Elem>
      <Oneof value={networkState}>
        <Elem name="loading" case="loading">
          <Spinner size={64}/>
        </Elem>
        <Elem name="content" case="loaded">
          {schsList.length ? (
            <PeopleList
              schsList={schsList}
              getSelectedRows={getSelectedRows}
            />
          ) : (
            <EmptySchsList openModal={openModal} />
          )}
          {modal && <CreateSch onClose={closeModal} />}
        </Elem>
      </Oneof>
    </Block>
  );
};

PeoplePage.title = "Schs";
PeoplePage.path = "/schs";
