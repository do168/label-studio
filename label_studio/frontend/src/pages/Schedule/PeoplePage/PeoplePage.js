import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useAPI } from "../../../providers/ApiProvider";
import { useConfig } from "../../../providers/ConfigProvider";
import { Block, Elem } from "../../../utils/bem";
import "./PeopleInvitation.styl";
import { PeopleList } from "./PeopleList";
import "./PeoplePage.styl";
import { SelectedUser } from "./SelectedUser";

export const PeoplePage = () => {
  const [selectedUser, setSelectedUser] = useState(null);

  const selectUser = useCallback((user) => {
    setSelectedUser(user);

    localStorage.setItem('selectedUser', user?.id);
  }, [setSelectedUser]);


  const defaultSelected = useMemo(() => {
    return localStorage.getItem('selectedUser');
  }, []);

  return (
    <Block name="people">
      <Elem name="content">
        <PeopleList
          selectedUser={selectedUser}
          defaultSelected={defaultSelected}
          onSelect={(user) => selectUser(user)}
        />

        {selectedUser && (
          <SelectedUser
            user={selectedUser}
            onClose={() => selectUser(null)}
          />
        )}
      </Elem>
    </Block>
  );
};

PeoplePage.title = "People";
PeoplePage.path = "/";
