% order5v2_0518  eq1=10721 eq2=36295  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,W),f(f(Y,X),Z))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(f(X,X),Y),f(Y,Y)),X) )).
