import React from 'react'
import { Card, Text, SimpleGrid, Group, Title } from '@mantine/core'
import {
  IconArrowUpRight,
  IconArrowDownRight,
  IconUsers,
  IconShoppingCart,
  IconCreditCard,
  IconReport,
  IconTrendingUp
} from '@tabler/icons-react'

const statsData = [
  {
    title: 'Total Page Views',
    value: '4,42,236',
    change: '+59.3%',
    positive: true,
    icon: IconReport,
    description: 'You made an extra 35,000 this year'
  },
  {
    title: 'Total Users',
    value: '78,250',
    change: '+70.5%',
    positive: true,
    icon: IconUsers,
    description: 'You made an extra 8,900 this year'
  },
  {
    title: 'Total Order',
    value: '18,800',
    change: '+27.4%',
    positive: true,
    icon: IconShoppingCart,
    description: 'You made an extra 1,943 this year'
  },
  {
    title: 'Total Sales',
    value: '35,078',
    change: '+27.4%',
    positive: true,
    icon: IconCreditCard,
    description: 'You made an extra 20,395 this year'
  }
]

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Welcome Card */}
      <Card
        withBorder
        p="xl"
        radius="md"
        className="bg-gradient-to-r from-blue-500 to-purple-600 text-white"
      >
        <Group justify="space-between">
          <div>
            <Title order={3} className="mb-2">
              Welcome back, John! 👋
            </Title>
            <Text size="sm" className="mb-4 opacity-90">
              Here&apos;s what&apos;s happening with your projects today
            </Text>
            <Group gap="xl">
              <div>
                <Text size="xs" className="opacity-75">
                  Total Revenue
                </Text>
                <Text size="xl" fw={700}>
                  $42,895
                </Text>
              </div>
              <div>
                <Text size="xs" className="opacity-75">
                  Growth
                </Text>
                <Group gap={4}>
                  <IconTrendingUp size={16} />
                  <Text size="xl" fw={700}>
                    +23.5%
                  </Text>
                </Group>
              </div>
            </Group>
          </div>
          <div className="text-6xl opacity-75">📊</div>
        </Group>
      </Card>

      {/* Stats Grid */}
      <SimpleGrid cols={{ base: 1, xs: 2, sm: 4 }} spacing="lg">
        {statsData.map((stat) => {
          const IconComponent = stat.icon
          return (
            <Card key={stat.title} withBorder p="lg" radius="md">
              <Group justify="space-between" mb="xs">
                <div className="bg-blue-50 p-2 rounded-lg">
                  <IconComponent size={20} className="text-blue-600" />
                </div>
                <Group gap={4}>
                  {stat.positive ? (
                    <IconArrowUpRight size={16} className="text-green-600" />
                  ) : (
                    <IconArrowDownRight size={16} className="text-red-600" />
                  )}
                  <Text
                    size="sm"
                    fw={500}
                    className={
                      stat.positive ? 'text-green-600' : 'text-red-600'
                    }
                  >
                    {stat.change}
                  </Text>
                </Group>
              </Group>
              <Text size="xs" c="dimmed" mb="xs">
                {stat.title}
              </Text>
              <Text fw={700} size="xl" mb="xs">
                {stat.value}
              </Text>
              <Text size="xs" c="dimmed">
                {stat.description}
              </Text>
            </Card>
          )
        })}
      </SimpleGrid>
    </div>
  )
}
