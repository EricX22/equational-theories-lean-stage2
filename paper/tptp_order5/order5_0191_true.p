% order5_0191  eq1=38286 eq2=19445  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,f(f(X,Y),Z)),Y),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(f(Z,W),f(Y,W))) )).
