import React from "react";
import { View, Text, Button } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../navigation/AppNavigator";

type Props = NativeStackScreenProps<RootStackParamList, "Settings">;

const SettingsScreen: React.FC<Props> = ({ navigation }) => {
  return (
    <View>
      <Text>Settings</Text>
      <Button title="Logout" onPress={() => navigation.replace("Login")} />
    </View>
  );
};

export default SettingsScreen;
