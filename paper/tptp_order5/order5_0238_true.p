% order5_0238  eq1=9698 eq2=36861  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Z,Y),f(Z,f(X,Z)))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),Y),f(X,W)),X) )).
