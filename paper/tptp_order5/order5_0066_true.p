% order5_0066  eq1=53496 eq2=23723  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(f(Z,X),W),Z),X) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),Y),f(Y,f(W,X))) )).
