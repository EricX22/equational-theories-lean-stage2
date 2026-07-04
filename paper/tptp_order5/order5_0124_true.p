% order5_0124  eq1=2093 eq2=23701  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,X),X),f(Z,X)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),Y),f(X,f(Y,W))) )).
