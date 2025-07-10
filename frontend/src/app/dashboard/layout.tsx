'use client'

import React from 'react'
import {
  AppShell,
  Avatar,
  Burger,
  Group,
  Menu,
  Text,
  UnstyledButton,
  ScrollArea,
  Box,
  ActionIcon,
  rem,
  Flex
} from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import {
  IconDashboard,
  IconUsers,
  IconMail,
  IconMessageCircle,
  IconSettings,
  IconChevronDown,
  IconLogout,
  IconUser,
  IconBell,
  IconLayoutSidebarLeftCollapse,
  IconLayoutSidebarRightCollapse
} from '@tabler/icons-react'
import Link from 'next/link'

// Navigation items with Tabler icons
const navItems = [
  {
    label: 'Dashboard',
    href: '/dashboard',
    icon: IconDashboard,
    color: 'blue'
  },
  {
    label: 'Users',
    href: '/dashboard/users',
    icon: IconUsers,
    color: 'green'
  },
  {
    label: 'Email',
    href: '/dashboard/email',
    icon: IconMail,
    color: 'orange'
  },
  {
    label: 'Chat',
    href: '/dashboard/chat',
    icon: IconMessageCircle,
    color: 'purple'
  },
  {
    label: 'Settings',
    href: '/dashboard/settings',
    icon: IconSettings,
    color: 'gray'
  }
]

export default function DashboardLayout({
  children
}: {
  children: React.ReactNode
}) {
  const [mobileOpened, { toggle: toggleMobile }] = useDisclosure()
  const [desktopOpened, { toggle: toggleDesktop }] = useDisclosure(true)

  return (
    <AppShell
      header={{ height: 60 }}
      navbar={{
        width: { base: 250, collapsed: 80 },
        breakpoint: 'sm',
        collapsed: { mobile: !mobileOpened }
      }}
      padding="md"
    >
      <AppShell.Header className="flex items-center justify-between px-4 border-b border-gray-200 bg-white">
        <Flex align="center" justify="flex-start" gap="sm">
          <Burger
            opened={mobileOpened}
            onClick={toggleMobile}
            hiddenFrom="sm"
            size="sm"
          />
          <div className="flex items-center gap-2">
            <Text size="lg" fw={700} c="blue">
              K12 R&D
            </Text>
          </div>
        </Flex>

        <Group gap="sm">
          <ActionIcon variant="transparent" size="lg" className="text-gray-600">
            <IconBell size={18} />
          </ActionIcon>

          <Menu shadow="md" width={200} position="bottom-end">
            <Menu.Target>
              <UnstyledButton className="flex items-center gap-2 px-2 py-1 rounded-md hover:bg-gray-100 transition-colors">
                <Avatar
                  src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100"
                  radius="xl"
                  size="sm"
                />
                <div className="hidden sm:block text-left">
                  <Text size="sm" fw={500}>
                    John Doe
                  </Text>
                  <Text size="xs" c="dimmed">
                    Administrator
                  </Text>
                </div>
                <IconChevronDown size={14} className="text-gray-500" />
              </UnstyledButton>
            </Menu.Target>

            <Menu.Dropdown>
              <Menu.Label>Account</Menu.Label>
              <Menu.Item leftSection={<IconUser size={14} />}>
                Profile
              </Menu.Item>
              <Menu.Item leftSection={<IconSettings size={14} />}>
                Settings
              </Menu.Item>
              <Menu.Divider />
              <Menu.Item leftSection={<IconLogout size={14} />} color="red">
                Logout
              </Menu.Item>
            </Menu.Dropdown>
          </Menu>
        </Group>
      </AppShell.Header>

      <AppShell.Navbar
        p={0}
        className="border-r border-gray-200 bg-white relative"
        style={{
          width: desktopOpened ? '250px' : '80px',
          transition: 'width 0.3s ease'
        }}
      >
        <ScrollArea className="flex-1">
          <Box p="md">
            <div className="space-y-1">
              {navItems.map((item) => {
                const IconComponent = item.icon
                const isActive = item.href === '/dashboard'

                return (
                  <Link href={item.href} key={item.label} className="block">
                    <UnstyledButton
                      className={`w-full rounded-md transition-all duration-200 ${
                        isActive
                          ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-500'
                          : 'hover:bg-gray-50 text-gray-700'
                      }`}
                      style={{
                        padding: rem(12),
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: desktopOpened ? 'flex-start' : 'center',
                        minHeight: rem(44),
                        position: 'relative'
                      }}
                      title={!desktopOpened ? item.label : undefined}
                    >
                      <div
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          width: rem(20),
                          height: rem(20),
                          flexShrink: 0
                        }}
                      >
                        <IconComponent
                          size={20}
                          className={`text-${item.color}-600`}
                        />
                      </div>
                      {desktopOpened && (
                        <Text
                          size="sm"
                          fw={500}
                          style={{
                            marginLeft: rem(12),
                            opacity: desktopOpened ? 1 : 0,
                            transition: 'opacity 0.2s ease'
                          }}
                        >
                          {item.label}
                        </Text>
                      )}
                    </UnstyledButton>
                  </Link>
                )
              })}
            </div>
          </Box>
        </ScrollArea>

        {/* Toggle button positioned at bottom right */}
        <Box className="absolute bottom-4 right-2">
          <ActionIcon
            onClick={toggleDesktop}
            variant="light"
            size="md"
            className="text-gray-600 hover:text-gray-900 shadow-md"
            radius="md"
          >
            {desktopOpened ? (
              <IconLayoutSidebarLeftCollapse size={18} />
            ) : (
              <IconLayoutSidebarRightCollapse size={18} />
            )}
          </ActionIcon>
        </Box>
      </AppShell.Navbar>

      <AppShell.Main className="bg-gray-50 min-h-screen">
        {children}
      </AppShell.Main>
    </AppShell>
  )
}
