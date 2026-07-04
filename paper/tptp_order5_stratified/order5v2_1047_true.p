% order5v2_1047  eq1=11448 eq2=16555  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,f(Y,Y)),f(W,W))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(f(f(Y,Z),Y),W),Z)) )).
