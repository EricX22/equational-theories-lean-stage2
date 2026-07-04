% order5v2_1950  eq1=40412 eq2=9991  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,f(Z,Y)),W),X),U) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(X,f(f(X,Y),f(f(Y,Z),W))) )).
