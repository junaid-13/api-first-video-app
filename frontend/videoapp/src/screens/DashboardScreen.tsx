import React, { useEffect, useState } from "react";
import { View, Text, FlatList, Image, TouchableOpacity, Button } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../../App";
import { fetchVideos } from "../services/api";

type Props = NativeStackScreenProps<RootStackParamList, "Dashboard">;

export default function DashboardScreen({ route, navigation }: Props) {
  const { token } = route.params;
  const [videos, setVideos] = useState<any[]>([]);

  useEffect(() => {
    fetchVideos(token).then((res) => {
      setVideos(res.videos.slice(0, 2)); // ONLY 2 videos
    });
  }, []);

  return (
    <View style={{ padding: 16 }}>
      <FlatList
        data={videos}
        keyExtractor={(item) => item._id}
        renderItem={({ item }) => (
          <TouchableOpacity
            onPress={() =>
              navigation.navigate("VideoPlayer", {
                videoId: item._id,
                token,
              })
            }
          >
            <Image
              source={{ uri: item.thumbnail }}
              style={{ height: 150, marginBottom: 8 }}
            />
            <Text style={{ fontSize: 18 }}>{item.title}</Text>
            <Text>{item.description}</Text>
          </TouchableOpacity>
        )}
      />

      <Button
        title="Settings"
        onPress={() => navigation.navigate("Settings", { token })}
      />
    </View>
  );
}
