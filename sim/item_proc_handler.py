from sim.character import Character
from sim.cooldowns import WrathOfCenariusBuff, EndlessGulchBuff
from sim.env import Environment
from sim.equipped_items import EquippedItems
from sim.item_procs import *
from sim.spell import Spell, SPELL_COEFFICIENTS
from sim.spell_school import DamageType


class ItemProcHandler:
    def __init__(self, character: Character, env: Environment, equipped_items: EquippedItems):
        self.character = character
        self.env = env

        self.procs = []

        self.wrath_of_cenarius_buff = None
        self.endless_gulch_buff = None

        self.wisdom_of_the_makaru_stacks = 0

        if equipped_items:
            if equipped_items.blade_of_eternal_darkness:
                self.procs.append(BladeOfEternalDarkness(character, self._blade_of_eternal_darkness_proc))
            if equipped_items.ornate_bloodstone_dagger:
                self.procs.append(OrnateBloodstoneDagger(character, self._ornate_bloodstone_dagger_proc))
            if equipped_items.wrath_of_cenarius:
                self.wrath_of_cenarius_buff = WrathOfCenariusBuff(character)
                self.procs.append(WrathOfCenarius(character, self._wrath_of_cenarius_proc))
            if equipped_items.endless_gulch:
                self.endless_gulch_buff = EndlessGulchBuff(character)
                self.procs.append(EndlessGulch(character, self._endless_gulch_proc))

    def check_for_procs(self, current_time):
        for proc in self.procs:
            proc.check_for_proc(current_time)

    def _tigger_proc_dmg(self, spell, min_dmg, max_dmg, damage_type):
        dmg = self.character.roll_spell_dmg(min_dmg, max_dmg, SPELL_COEFFICIENTS.get(spell, 0), damage_type)
        dmg = self.character.modify_dmg(dmg, damage_type, is_periodic=False)

        partial_amount = self.character.roll_partial(is_dot=False, is_binary=False)
        partial_desc = ""
        if partial_amount < 1:
            dmg = int(dmg * partial_amount)
            partial_desc = f"({int(partial_amount * 100)}% partial)"
            if hasattr(self.character, "arcane_surge_cd"):
                self.character.arcane_surge_cd.enable_due_to_partial_resist()

        # 100 flat shadow damage
        self.character.print(f"{spell.value} {partial_desc} {dmg}")
        self.env.total_spell_dmg += dmg
        self.env.meter.register(self.character.name, dmg)

        self.character.num_casts[spell] = self.character.num_casts.get(spell, 0) + 1


    def _blade_of_eternal_darkness_proc(self):
        self._tigger_proc_dmg(Spell.ENGULFING_SHADOWS, 100, 100, DamageType.SHADOW)

    def _ornate_bloodstone_dagger_proc(self):
        self._tigger_proc_dmg(Spell.BURNING_HATRED, 250, 250, DamageType.FIRE)

    def _wrath_of_cenarius_proc(self):
        if self.wrath_of_cenarius_buff:
            self.wrath_of_cenarius_buff.activate()

    def _endless_gulch_proc(self):
        self.wisdom_of_the_makaru_stacks += 1
        self.character.print(f"Wisdom of the Makaru proc {self.wisdom_of_the_makaru_stacks}")
        if self.wisdom_of_the_makaru_stacks >= 10:
            self.wisdom_of_the_makaru_stacks = 0
            if self.endless_gulch_buff:
                self.endless_gulch_buff.activate()
