% order5v2_1789  eq1=10636 eq2=30750  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,Z),f(f(Y,X),W))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(Z,f(f(Y,Z),Y))),Z) )).
