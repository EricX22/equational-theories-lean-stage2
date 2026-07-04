% order5_0061  eq1=61616 eq2=40122  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(f(X,Y),Z) = f(f(W,f(Z,Y)),X) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,f(X,Z)),W),W),U) )).
