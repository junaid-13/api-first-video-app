import React from "react";
import { View, Text } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../navigation/AppNavigator";

type Props = NativeStackScreenProps<RootStackParamList, "Dashboard">;

const DashboardScreen: React.FC<Props> = ({ navigation }) => {
  return (
    <View>
      <Text>Dashboard</Text>
    </View>
  );
};

export default DashboardScreen;
