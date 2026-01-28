import React from "react";
import { View, Text, Button } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../../App";

type Props = NativeStackScreenProps<RootStackParamList, "Settings">;

export default function SettingsScreen({ navigation }: Props) {
  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 18 }}>Username: Test User</Text>
      <Text style={{ marginBottom: 20 }}>Email: test@example.com</Text>

      <Button
        title="Logout"
        onPress={() => navigation.replace("Login")}
      />
    </View>
  );
}
