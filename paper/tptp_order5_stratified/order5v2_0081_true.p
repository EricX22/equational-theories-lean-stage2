% order5v2_0081  eq1=13891 eq2=2637  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(Y,f(f(Y,Z),W)),W)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(Y,f(f(Z,W),W)),U) )).
