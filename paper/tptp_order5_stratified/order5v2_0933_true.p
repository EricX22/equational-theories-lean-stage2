% order5v2_0933  eq1=8713 eq2=53560  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(Z,f(f(f(X,X),Y),Y))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(f(Z,Y),Z),W),Z) )).
