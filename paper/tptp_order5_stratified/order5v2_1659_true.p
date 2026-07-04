% order5v2_1659  eq1=47411 eq2=62189  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(f(Z,Y),f(f(Z,Y),X)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(f(X,Y),Y) = f(f(f(Z,W),Z),X) )).
