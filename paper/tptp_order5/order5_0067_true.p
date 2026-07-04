% order5_0067  eq1=19843 eq2=13490  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(Y,X),f(f(X,f(Z,W)),U)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(X,f(f(X,f(f(Y,Y),X)),X)) )).
