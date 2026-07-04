% order5_0008  eq1=36908 eq2=26329  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),Y),f(W,Y)),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(f(Z,Y),X)),f(Y,X)) )).
